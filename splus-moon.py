#!/usr/bin/env python

import sys
import numpy as np
import astropy.units as u
from os.path import basename
from astropy.time import Time
from zoneinfo import ZoneInfo
from astropy.io.fits import getheader
from datetime import datetime, timedelta
from astropy.coordinates import AltAz, EarthLocation, SkyCoord, get_sun, get_moon

__script_name__ = basename(sys.argv[0])

def get_location_moon_illumination(location_time, return_moon=False):
    sun = get_sun(location_time)
    moon = get_moon(location_time)
    elongation = sun.separation(moon)
    moon_phase_angle = np.arctan2(
        sun.distance*np.sin(elongation), 
        moon.distance - sun.distance*np.cos(elongation)
    )
    moon_illumination = (1 + np.cos(moon_phase_angle))/2.0    
    if return_moon:
        return moon_illumination, moon
    return moon_illumination

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except:
        print('Usage: ./{} FITSFILE'.format(__script_name__))
        sys.exit(1)
    date_fmt = '%Y-%m-%d'
    time_fmt = '%H:%M:%S.%f'
    datetime_fmt = '{}T{}'.format(date_fmt, time_fmt)
    datetime_fmt_zoneinfo = '{} %z'.format(datetime_fmt)

    hdr = getheader(filename, 1)

    t80s_coordinates = {
        'HEI': eval(hdr.get('HIERARCH T80S TEL GEOELEV'))*u.m,
        'LAT': eval(hdr.get('HIERARCH T80S TEL GEOLAT'))*u.deg,
        'LON': eval(hdr.get('HIERARCH T80S TEL GEOLON'))*u.deg,
    }    
    t80s_zoneinfo = 'America/Santiago'

    t80s_EL = EarthLocation(
        lat=t80s_coordinates['LAT'], 
        lon=t80s_coordinates['LON'], 
        height=t80s_coordinates['HEI']
    )

    str_dt_obs = hdr.get('DATE-OBS', None)
    str_time_obs = hdr.get('TIME', None)
    str_time_obs = str_time_obs.split(' to ')
    str_time_ini_obs, str_time_fin_obs = str_time_obs
    #print('str_dt_obs: ', str_dt_obs)
    #print('str_time_obs: ', str_time_obs)
    #print('str_time_ini_obs: ', str_time_ini_obs)
    #print('str_time_fin_obs: ', str_time_fin_obs)

    # CALC OBS DURATION IN SECONDS
    time_ini_obs = datetime.strptime(str_time_ini_obs, time_fmt)
    time_fin_obs = datetime.strptime(str_time_fin_obs, time_fmt)
    obs_duration_seconds = (time_fin_obs - time_ini_obs).total_seconds()
    #print('obs_duration_seconds: ', obs_duration_seconds)
    if obs_duration_seconds < 0:
        time_fin_obs += timedelta(days=1)
        obs_duration_seconds = (time_fin_obs - time_ini_obs).total_seconds()
    #print('obs_duration_seconds: ', obs_duration_seconds)

    # DATETIME OBS UTC
    dt_obs = datetime.strptime(str_dt_obs + ' +00:00', datetime_fmt_zoneinfo)
    #print('dt_obs: ', dt_obs)
    #print('ZoneInfo: ', dt_obs.tzinfo)

    # DATETIME OBS T80-S
    t80s_dt_obs = dt_obs.astimezone(ZoneInfo(t80s_zoneinfo))
    #print('T80S DATETIME OBS: ', t80s_dt_obs)
    #print('T80S DATETIME OBS ZoneInfo: ', t80s_dt_obs.tzinfo)    

    # DATETIME INI OBS T80-S
    str_dt_ini_obs = '{}T{} {}'.format(
        t80s_dt_obs.strftime(datetime_fmt.split('T')[0]), 
        str_time_ini_obs, 
        t80s_dt_obs.strftime('%z')
    )
    #print('str_dt_ini_obs: ', str_dt_ini_obs)
    dt_ini_obs = datetime.strptime(str_dt_ini_obs, datetime_fmt_zoneinfo).replace(tzinfo=ZoneInfo(t80s_zoneinfo))
    #print('dt_ini_obs: ', dt_ini_obs)
    delta_time = (dt_ini_obs - t80s_dt_obs).total_seconds()
    #print('delta_time: ', delta_time)
    if (delta_time < 0):
        dt_ini_obs += timedelta(days=1)
        delta_time = (dt_ini_obs - t80s_dt_obs).total_seconds()
        #print('delta_time: ', delta_time)
    #print('dt_ini_obs: ', dt_ini_obs)
    print('T80S DATETIME INI OBS: ', dt_ini_obs)
    t80s_T_ini_obs = Time(dt_ini_obs, location=t80s_EL)# - utc_offset_hours
    #print('t80s_T_ini_obs: ', t80s_T_ini_obs)

    str_dt_fin_obs = '{}T{} {}'.format(
        t80s_dt_obs.strftime(datetime_fmt.split('T')[0]), 
        str_time_fin_obs, 
        t80s_dt_obs.strftime('%z')
    )
    #print('str_dt_fin_obs: ', str_dt_fin_obs)
    dt_fin_obs = datetime.strptime(str_dt_fin_obs, datetime_fmt_zoneinfo).replace(tzinfo=ZoneInfo('America/Santiago'))
    #print('dt_fin_obs: ', dt_fin_obs)
    delta_time = (dt_fin_obs - dt_ini_obs).total_seconds()
    #print('delta_time: ', delta_time)
    if (delta_time < 0):
        dt_fin_obs += timedelta(days=1)
        delta_time = (dt_fin_obs - dt_ini_obs).total_seconds()
        print('delta_time: ', delta_time)
    #print('dt_fin_obs: ', dt_fin_obs)

    try:
        assert(delta_time == obs_duration_seconds)
    except:
        print('{}: Calculated OBS duration problem.'.format(__script_name__))

    t80s_T_fin_obs = Time(dt_fin_obs, location=t80s_EL)# - utc_offset_hours
    #print('t80s_T_fin_obs: ', t80s_T_fin_obs)

    c = SkyCoord(ra=hdr['ra'], dec=hdr['dec'], unit=(u.hourangle, u.deg))
    cT_ini = c.transform_to(AltAz(obstime=t80s_T_ini_obs, location=t80s_EL))
    cT_fin = c.transform_to(AltAz(obstime=t80s_T_fin_obs, location=t80s_EL))
    moon_t80s_ini_illumination, moon_t80s_ini = get_location_moon_illumination(t80s_T_ini_obs, return_moon=True)
    moon_t80_ini_sep = cT_ini.separation(moon_t80s_ini)
    moon_t80s_fin_illumination, moon_t80s_fin = get_location_moon_illumination(t80s_T_fin_obs, return_moon=True)
    moon_t80s_fin_sep = cT_fin.separation(moon_t80s_fin)
    mms = 0.5*(moon_t80s_fin_sep + moon_t80_ini_sep)
    mmi = 0.5*(moon_t80s_fin_illumination + moon_t80s_ini_illumination)

    ##########################################
    ############## FINAL DIGEST ##############
    ##########################################
    print('OBJECT COORD (RA, DEC) : ({}, {})'.format(c.ra, c.dec))
    print('T80S DATETIME OBS: ', t80s_dt_obs)
    print('T80S DATETIME OBS ZoneInfo: ', t80s_dt_obs.tzinfo)    
    print('T80S DATETIME INI OBS: ', dt_ini_obs)
    print('OBJECT COORD INI OBS (ALT, AZ) : ({}, {})'.format(cT_ini.alt, cT_ini.az))
    print('MOON SEPARATION INI OBS: {:.5f}'.format(moon_t80_ini_sep))
    print('MOON ILLUMINATION INI OBS: {:.5f}'.format(moon_t80s_ini_illumination))
    print('T80S DATETIME END OBS: ', dt_fin_obs)
    print('\tOBS DURATION: ', delta_time)
    print('OBJECT COORD END OBS (ALT, AZ) : ({}, {})'.format(cT_fin.alt, cT_fin.az))
    print('MOON SEPARATION END OBS: {:.5f}'.format(moon_t80s_fin_sep))
    print('MOON ILLUMINATION END OBS: {:.5f}'.format(moon_t80s_fin_illumination))
    print('MEAN MOON SEPARATION: {:.5f}'.format(mms))
    print('MEAN MOON ILLUMINATION: {:.5f}'.format(mmi))
    ##########################################
    ##########################################
    ##########################################
