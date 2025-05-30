
# Magic Numbers for Target Index TLV
TRACK_INDEX_WEAK_SNR = 253 # Point not associated, SNR too weak
TRACK_INDEX_BOUNDS = 254 # Point not associated, located outside boundary of interest
TRACK_INDEX_NOISE = 255 # Point not associated, considered as noise

# Defined TLV's
MMWDEMO_OUTPUT_MSG_DETECTED_POINTS                      = 1
MMWDEMO_OUTPUT_MSG_RANGE_PROFILE                        = 2
MMWDEMO_OUTPUT_MSG_NOISE_PROFILE                        = 3
MMWDEMO_OUTPUT_MSG_AZIMUT_STATIC_HEAT_MAP               = 4
MMWDEMO_OUTPUT_MSG_RANGE_DOPPLER_HEAT_MAP               = 5
MMWDEMO_OUTPUT_MSG_STATS                                = 6
MMWDEMO_OUTPUT_MSG_DETECTED_POINTS_SIDE_INFO            = 7
MMWDEMO_OUTPUT_MSG_AZIMUT_ELEVATION_STATIC_HEAT_MAP     = 8
MMWDEMO_OUTPUT_MSG_TEMPERATURE_STATS                    = 9

# xWRL6432 Out-of-box demo packets
MMWDEMO_OUTPUT_EXT_MSG_DETECTED_POINTS                  = 301
MMWDEMO_OUTPUT_EXT_MSG_RANGE_PROFILE_MAJOR              = 302
MMWDEMO_OUTPUT_EXT_MSG_RANGE_PROFILE_MINOR              = 303
MMWDEMO_OUTPUT_EXT_MSG_RANGE_AZIMUT_HEAT_MAP_MAJOR      = 304
MMWDEMO_OUTPUT_EXT_MSG_RANGE_AZIMUT_HEAT_MAP_MINOR      = 305
MMWDEMO_OUTPUT_MSG_EXT_STATS                            = 306
MMWDEMO_OUTPUT_EXT_MSG_PRESENCE_INFO                    = 307
MMWDEMO_OUTPUT_EXT_MSG_TARGET_LIST                      = 308
MMWDEMO_OUTPUT_EXT_MSG_TARGET_INDEX                     = 309
MMWDEMO_OUTPUT_EXT_MSG_MICRO_DOPPLER_RAW_DATA           = 310
MMWDEMO_OUTPUT_EXT_MSG_MICRO_DOPPLER_FEATURES           = 311
MMWDEMO_OUTPUT_EXT_MSG_RADAR_CUBE_MAJOR                 = 312
MMWDEMO_OUTPUT_EXT_MSG_RADAR_CUBE_MINOR                 = 313
MMWDEMO_OUTPUT_EXT_MSG_POINT_CLOUD_INDICES              = 314
MMWDEMO_OUTPUT_EXT_MSG_ENHANCED_PRESENCE_INDICATION     = 315
MMWDEMO_OUTPUT_EXT_MSG_ADC_SAMPLES                      = 316
MMWDEMO_OUTPUT_EXT_MSG_CLASSIFIER_INFO                  = 317
MMWDEMO_OUTPUT_EXT_MSG_RX_CHAN_COMPENSATION_INFO        = 318
MMWDEMO_OUTPUT_EXT_MSG_QUICK_EVAL_INFO                  = 319
MMWDEMO_OUTPUT_EXT_MSG_POINT_CLOUD_ANTENNA_SYMBOLS      = 320
MMWDEMO_OUTPUT_EXT_MSG_MODE_SWITCH_INFO                 = 321

MMWDEMO_OUTPUT_MSG_GESTURE_FEATURES_6432                = 350
MMWDEMO_OUTPUT_MSG_GESTURE_CLASSIFIER_6432              = 351
MMWDEMO_OUTPUT_MSG_GESTURE_PRESENCE_x432                = 352
MMWDEMO_OUTPUT_MSG_GESTURE_PRESENCE_THRESH_x432         = 353
MMWDEMO_OUTPUT_EXT_MAGNITUDE                            = 354
MMWDEMO_OUTPUT_EXT_RANGEIDX                             = 355
MMWDEMO_OUTPUT_EXT_ELEVIDX                              = 356
MMWDEMO_OUTPUT_EXT_AZIMIDX                              = 357

MMWDEMO_OUTPUT_MSG_SPHERICAL_POINTS                     = 1000
MMWDEMO_OUTPUT_MSG_TRACKERPROC_3D_TARGET_LIST           = 1010
MMWDEMO_OUTPUT_MSG_TRACKERPROC_TARGET_INDEX             = 1011
MMWDEMO_OUTPUT_MSG_TRACKERPROC_TARGET_HEIGHT            = 1012
MMWDEMO_OUTPUT_MSG_COMPRESSED_POINTS                    = 1020
MMWDEMO_OUTPUT_MSG_PRESCENCE_INDICATION                 = 1021
MMWDEMO_OUTPUT_MSG_OCCUPANCY_STATE_MACHINE              = 1030
MMWDEMO_OUTPUT_MSG_SURFACE_CLASSIFICATION               = 1031
MMWDEMO_OUTPUT_EXT_MSG_VELOCITY                         = 1033
MMWDEMO_OUTPUT_EXT_MSG_STATS_BSD                        = 1034
MMWDEMO_OUTPUT_EXT_MSG_TARGET_LIST_2D_BSD               = 1035


MMWDEMO_OUTPUT_MSG_VITALSIGNS                           = 1040

MMWDEMO_OUTPUT_MSG_GESTURE_FEATURES_6843                = 1050
MMWDEMO_OUTPUT_MSG_GESTURE_OUTPUT_PROB_6843             = 1051

MMWDEMO_OUTPUT_EXT_MSG_CAM_TRIGGERS                     = 3000