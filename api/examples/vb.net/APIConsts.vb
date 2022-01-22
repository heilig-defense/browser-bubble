Public Module APIConsts
    Public Const BB_SERVER_ACTION_STATUS As Integer = 0
    Public Const BB_SERVER_STATUS_SUB_ACTION_CURRENT As Integer = 1
    Public Const BB_SERVER_STATUS_SUB_ACTION_SHUTDOWN As Integer = 2
    Public Const BB_SERVER_STATUS_SUB_ACTION_LOG As Integer = 3

    Public Const BB_SERVER_ACTION_OPTIONS As Integer = 1
    Public Const BB_SERVER_OPTIONS_SUB_ACTION_SET_OP_VALUE As Integer = 1
    Public Const BB_SERVER_OPTIONS_SUB_ACTION_GET_OP_VALUE As Integer = 2
    Public Const BB_SERVER_OPTIONS_SUB_ACTION_REINIT As Integer = 3

    Public Const BB_SERVER_ACTION_BROWSER As Integer = 2
    Public Const BB_SERVER_BROWSER_SUB_ACTION_SYS_QUERY As Integer = 1
    Public Const BB_SERVER_BROWSER_SUB_ACTION_LIST As Integer = 2
    Public Const BB_SERVER_BROWSER_SUB_ACTION_ADD As Integer = 3
    Public Const BB_SERVER_BROWSER_SUB_ACTION_DELETE As Integer = 4
    Public Const BB_SERVER_BROWSER_SUB_ACTION_UPDATE As Integer = 5

    Public Const BB_SERVER_ACTION_SPEECH As Integer = 3
    Public Const BB_SERVER_SPEECH_SUB_ACTION_LIST As Integer = 1
    Public Const BB_SERVER_SPEECH_SUB_ACTION_CREATE As Integer = 2
    Public Const BB_SERVER_SPEECH_SUB_ACTION_DELETE As Integer = 3
    Public Const BB_SERVER_SPEECH_SUB_ACTION_UPDATE As Integer = 4

    Public Const BB_SERVER_ACTION_FONT As Integer = 4
    Public Const BB_SERVER_FONT_SUB_ACTION_LIST As Integer = 1
    Public Const BB_SERVER_FONT_SUB_ACTION_CREATE As Integer = 2
    Public Const BB_SERVER_FONT_SUB_ACTION_DELETE As Integer = 3
    Public Const BB_SERVER_FONT_SUB_ACTION_UPDATE As Integer = 4
    Public Const BB_SERVER_FONT_SUB_ACTION_INSTALL As Integer = 5

    Public Const BB_SERVER_ACTION_DNS As Integer = 5
    Public Const BB_SERVER_DNS_SUB_ACTION_SYNC As Integer = 1
    Public Const BB_SERVER_DNS_SUB_ACTION_LIST As Integer = 2
    Public Const BB_SERVER_DNS_SUB_ACTION_CREATE As Integer = 3
    Public Const BB_SERVER_DNS_SUB_ACTION_DELETE As Integer = 4
    Public Const BB_SERVER_DNS_SUB_ACTION_UPDATE As Integer = 5
    Public Const BB_SERVER_DNS_SUB_ACTION_SINKHOLE_SEARCH As Integer = 6

    Public Const BB_SERVER_ACTION_PROXY As Integer = 6
    Public Const BB_SERVER_PROXY_SUB_ACTION_LIST As Integer = 1
    Public Const BB_SERVER_PROXY_SUB_ACTION_CREATE As Integer = 2
    Public Const BB_SERVER_PROXY_SUB_ACTION_DELETE As Integer = 3
    Public Const BB_SERVER_PROXY_SUB_ACTION_UPDATE As Integer = 4

    Public Const BB_SERVER_ACTION_VPN As Integer = 7
    Public Const BB_SERVER_VPN_SUB_ACTION_LIST As Integer = 1
    Public Const BB_SERVER_VPN_SUB_ACTION_CREATE As Integer = 2
    Public Const BB_SERVER_VPN_SUB_ACTION_DELETE As Integer = 3
    Public Const BB_SERVER_VPN_SUB_ACTION_UPDATE As Integer = 4

    Public Const BB_SERVER_ACTION_BUBBLE As Integer = 8
    Public Const BB_SERVER_BUBBLE_SUB_ACTION_LIST_SAVED As Integer = 1
    Public Const BB_SERVER_BUBBLE_SUB_ACTION_LIST_RUNNING As Integer = 2
    Public Const BB_SERVER_BUBBLE_SUB_ACTION_CREATE As Integer = 3
    Public Const BB_SERVER_BUBBLE_SUB_ACTION_DELETE As Integer = 4
    Public Const BB_SERVER_BUBBLE_SUB_ACTION_UPDATE As Integer = 5
    Public Const BB_SERVER_BUBBLE_SUB_ACTION_DETAILS As Integer = 6
    Public Const BB_SERVER_BUBBLE_SUB_ACTION_GENERATE As Integer = 7
    Public Const BB_SERVER_BUBBLE_SUB_ACTION_SHORTCUT As Integer = 8
    Public Const BB_SERVER_BUBBLE_SUB_ACTION_LAUNCH As Integer = 9
    Public Const BB_SERVER_BUBBLE_SUB_ACTION_TERMINATE As Integer = 10
    Public Const BB_SERVER_BUBBLE_SUB_ACTION_NETWORK As Integer = 11
    Public Const BB_SERVER_BUBBLE_SUB_ACTION_READY As Integer = 12
    Public Const BB_SERVER_BUBBLE_SUB_ACTION_FAILED As Integer = 13
    Public Const BB_SERVER_BUBBLE_SUB_ACTION_SHUTDOWN As Integer = 14
    Public Const BB_SERVER_BUBBLE_SUB_ACTION_DEBUG_PORT As Integer = 15
    
    Public Const BB_SERVER_ACTION_LAUNCH As Integer = 9
    Public Const BB_SERVER_LAUNCH_SUB_ACTION_LIST As Integer = 1
    Public Const BB_SERVER_LAUNCH_SUB_ACTION_CREATE As Integer = 2
    Public Const BB_SERVER_LAUNCH_SUB_ACTION_DELETE As Integer = 3
    Public Const BB_SERVER_LAUNCH_SUB_ACTION_UPDATE As Integer = 4

    Public Const BB_OS_DISABLED As Integer = 0
    Public Const BB_OS_WIN7 As Integer = 1
    Public Const BB_OS_WIN8 As Integer = 2
    Public Const BB_OS_WIN81 As Integer = 4
    Public Const BB_OS_WIN10 As Integer = 8
    Public Const BB_OS_WIN11 As Integer = 16
    Public Const BB_OS_CUSTOM As Integer = 32

    Public Const BB_DATA_TYPE_STRING As Integer = 1
    Public Const BB_DATA_TYPE_INTEGER As Integer = 2
    Public Const BB_DATA_TYPE_JSON As Integer = 3
    Public Const BB_DATA_TYPE_BINARY As Integer = 4
    Public Const BB_DATA_TYPE_BASE64 As Integer = 5

    Public Const BB_ERROR_NO_ERROR As Integer = 0
    Public Const BB_ERROR_GENERIC_ERROR As Integer = -1
    Public Const BB_ERROR_INVALID_PARAMETER As Integer = -3
    Public Const BB_ERROR_INVALID_MODE As Integer = -26
    Public Const BB_ERROR_CREATING_PROCESS As Integer = -30
    Public Const BB_ERROR_NOT_READY As Integer = -34
    Public Const BB_ERROR_LICENSE_INVALID As Integer = -361

    Public Const BB_LOG_LEVEL_DEBUG As Integer = 1
    Public Const BB_LOG_LEVEL_ERROR As Integer = 2
    Public Const BB_LOG_LEVEL_INFO As Integer = 3
    Public Const BB_LOG_LEVEL_WARN As Integer = 4
    Public Const BB_LOG_LEVEL_PRIORITY As Integer = 5

    Public Const BB_OPTIONS_XET_FLAGS As Integer = 1
    Public Const BB_OPTIONS_XET_LICENSE As Integer = 2
    Public Const BB_OPTIONS_XET_ADAPTER As Integer = 3
    Public Const BB_OPTIONS_XET_ADAPTER_LIST As Integer = 4
    Public Const BB_OPTIONS_XET_GLOBAL_DNS As Integer = 5
    Public Const BB_OPTIONS_XET_GLOBAL_AEX As Integer = 6

    Public Const BB_OPTIONS_FLAG_AUTO_BUBBLE As Integer = 1
    Public Const BB_OPTIONS_FLAG_BLOCK_NET As Integer = 2
    Public Const BB_OPTIONS_FLAG_TERMINATE_ON_EXIT As Integer = 4
    Public Const BB_OPTIONS_FLAG_DELETE_PROFILE As Integer = 8
    Public Const BB_OPTIONS_FLAG_USE_VHD_SANDBOX As Integer = 16
    Public Const BB_OPTIONS_FLAG_VERBOSE_DNS_LOG As Integer = 32

    Public Const BB_LICENSE_STATUS_INVALID As Integer = 0
    Public Const BB_LICENSE_STATUS_VALID As Integer = 1
    Public Const BB_LICENSE_STATUS_TRIAL As Integer = 2
    Public Const BB_LICENSE_STATUS_EXPIRED As Integer = 3
    Public Const BB_LICENSE_STATUS_REVOKED As Integer = 4

    Public Const BB_LICENSE_ENTITLEMENT_SINGLE_SYSTEM As Integer = 1
    Public Const BB_LICENSE_ENTITLEMENT_MULTI_SYSTEM As Integer = 2
    Public Const BB_LICENSE_ENTITLEMENT_COUNT_LIMITED As Integer = 4
    Public Const BB_LICENSE_ENTITLEMENT_SERVER_ENABLED As Integer = 8

    Public Const BB_FONT_OP_PROFILE As Integer = 1
    Public Const BB_FONT_OP_FONT_ITEM As Integer = 2

    ' Action is defined to run before the Bubble launches.
    Public Const BB_LAUNCH_ACTION_OP_START_PRE As Integer = 1
    ' Action is defined to run right after the Bubble launches.
    Public Const BB_LAUNCH_ACTION_OP_START_POST As Integer = 2
    ' Action is defined to run after the Bubble shuts down.
    Public Const BB_LAUNCH_ACTION_OP_START_CLOSE As Integer = 4
    ' Browser Bubble will not wait for the process to finish.
    Public Const BB_LAUNCH_ACTION_OP_WAIT_NONE As Integer = 8
    ' Browser Bubble will wait for the process to finish or until the 'Timeout' value is reached.
    Public Const BB_LAUNCH_ACTION_OP_WAIT_COMPLETE As Integer = 16
    ' Browser Bubble will evaluate the output of the process in relation to the set 'EvalValue' field.
    Public Const BB_LAUNCH_ACTION_OP_WAIT_EVAL As Integer = 32
    ' Output must match 'EvalValue' exactly.
    Public Const BB_LAUNCH_ACTION_OP_EVAL_IS As Integer = 64
    ' Output must not match 'EvalValue' exactly.
    Public Const BB_LAUNCH_ACTION_OP_EVAL_IS_NOT As Integer = 128
    ' Output must contain 'EvalValue'
    Public Const BB_LAUNCH_ACTION_OP_EVAL_CONTAINS As Integer = 256
    ' Output must not contain 'EvalValue'
    Public Const BB_LAUNCH_ACTION_OP_EVAL_CONTAINS_NOT As Integer = 512
    ' If the eval returns TRUE or the Timeout is reached then the Bubble will be cancelled.
    ' If the eval returns FALSE then the Bubble will continue to launch.
    ' This only applies for Pre actions.
    Public Const BB_LAUNCH_ACTION_OP_ACTION_CANCEL As Integer = 1024
    ' If the eval returns FALSE or the Timeout is reached then the Bubble will continue to launch.
    ' If the eval returns TRUE, then the Bubble will continue to launch.
    ' This only applies for Pre actions.
    Public Const BB_LAUNCH_ACTION_OP_ACTION_IGNORE As Integer = 2048

    Public Const BB_SPEECH_PROFILE As Integer = 1
    Public Const BB_SPEECH_VOICE As Integer = 2
    Public Const BB_SPEECH_PROFILE_VOICES As Integer = 3

    Public Const BB_SPEECH_AGE_ADULT As Integer = 1
    Public Const BB_SPEECH_AGE_CHILD As Integer = 2

    Public Const BB_SPEECH_SEX_FEMALE As Integer = 1
    Public Const BB_SPEECH_SEX_MALE As Integer = 2
    
    Public Const BB_GENERATE_COLOR_BORDER As Integer = 1
    Public Const BB_GENERATE_DEBUG_PORTS As Integer = 2

    Public Const BB_BROWSER_FIREFOX As Integer = 1
    Public Const BB_BROWSER_EDGE As Integer = 2
    Public Const BB_BROWSER_CHROME As Integer = 4
    Public Const BB_BROWSER_BLISK As Integer = 8
    Public Const BB_BROWSER_BRAVE As Integer = 16
    Public Const BB_BROWSER_CANARY As Integer = 32
    Public Const BB_BROWSER_CHROMIUM As Integer = 64
    Public Const BB_BROWSER_IRIDIUM As Integer = 128
    Public Const BB_BROWSER_IRON As Integer = 256
    Public Const BB_BROWSER_OPERA As Integer = 512
    Public Const BB_BROWSER_VIVALDI As Integer = 1024
    Public Const BB_BROWSER_FIREFOX_NIGHTLY As Integer = 2048
    Public Const BB_BROWSER_EPIC As Integer = 4096
    'User defined browsers.
    Public Const BB_BROWSER_EXTRA_1 As Integer = 262144
    Public Const BB_BROWSER_EXTRA_2 As Integer = 524288
    Public Const BB_BROWSER_EXTRA_3 As Integer = 1048576
    Public Const BB_BROWSER_EXTRA_4 As Integer = 2097152
    Public Const BB_BROWSER_EXTRA_5 As Integer = 4194304
    Public Const BB_BROWSER_EXTRA_6 As Integer = 8388608
    Public Const BB_BROWSER_EXTRA_7 As Integer = 16777216
    Public Const BB_BROWSER_EXTRA_8 As Integer = 33554432

    Public Const BB_BROWSER_UPDATE_ENABLE As Integer = 1
    Public Const BB_BROWSER_UPDATE_PROFILE As Integer = 2

    Public Const BB_DNS_TYPE_DNS_OVER_TLS As Integer = 1
    Public Const BB_DNS_TYPE_DNS_OVER_HTTPS As Integer = 2

    Public Const BB_PROXY_TYPE_HTTPS As Integer = 1
    Public Const BB_PROXY_TYPE_SOCKS4 As Integer = 2
    Public Const BB_PROXY_TYPE_SOCKS5 As Integer = 3

    Public Const BB_BATTERY_FLAG_PLUGGED_IN As Integer = 1
    Public Const BB_BATTERY_FLAG_BATTERY_POWER As Integer = 2
    Public Const BB_BATTERY_FLAG_NO_BATTERY As Integer = 4

    Public Const BB_FONT_OPS_DISABLE As Integer = 1
    Public Const BB_FONT_OPS_REMOVE_ALL_BUT_1 As Integer = 2
    Public Const BB_FONT_OPS_REMOVE_ALL_BUT_DEFINED As Integer = 4
    Public Const BB_FONT_OPS_SET_OS As Integer = 8
    Public Const BB_FONT_OPS_SET_CUSTOM As Integer = 16

    Public Const BB_MATH_SPOOFING_OFF As Integer = 0
    Public Const BB_MATH_SPOOFING_RANDOM As Integer = 1
    Public Const BB_MATH_SPOOFING_SET As Integer = 2

    Public Const BB_MEDIA_DEVICE_SPOOF_OFF As Integer = 0
    Public Const BB_MEDIA_DEVICE_ENUM_RANDOM As Integer = 1
    Public Const BB_MEDIA_DEVICE_ENUM_BLOCK As Integer = 2
    Public Const BB_MEDIA_DEVICE_RENAME_NAMES As Integer = 4
    Public Const BB_MEDIA_DEVICE_SET_SAMPLE As Integer = 8

    Public Const BB_WEBGL_SPOOFING_OFF As Integer = 0
    Public Const BB_WEBGL_SET_FEATURE_LEVEL As Integer = 1
    Public Const BB_WEBGL_SET_IMAGE_RGB As Integer = 2
    Public Const BB_WEBGL_RANDOMIZE_IMAGE_RBG As Integer = 4

    Public Const BB_WEBGL_LEVEL_9_1 As Integer = 1
    Public Const BB_WEBGL_LEVEL_9_2 As Integer = 2
    Public Const BB_WEBGL_LEVEL_9_3 As Integer = 3
    Public Const BB_WEBGL_LEVEL_10_0 As Integer = 4
    Public Const BB_WEBGL_LEVEL_10_1 As Integer = 5
    Public Const BB_WEBGL_LEVEL_11_0 As Integer = 6
    Public Const BB_WEBGL_LEVEL_11_1 As Integer = 7
    Public Const BB_WEBGL_LEVEL_12_0 As Integer = 8
    Public Const BB_WEBGL_LEVEL_12_1 As Integer = 9

    Public Const BB_BUBBLE_SPOOF_TIMEZONE As Integer = 1
    Public Const BB_BUBBLE_SPOOF_SCREEN As Integer = 2
    Public Const BB_BUBBLE_SPOOF_CPU_COUNT As Integer = 3
    Public Const BB_BUBBLE_SPOOF_MEMORY As Integer = 4
    Public Const BB_BUBBLE_SPOOF_TOUCHPOINTS As Integer = 5
    Public Const BB_BUBBLE_SPOOF_FONTS As Integer = 6
    Public Const BB_BUBBLE_SPOOF_LANGUAGE As Integer = 7
    Public Const BB_BUBBLE_SPOOF_PLATFORM As Integer = 8
    ' RESERVED As Integer = 9
    Public Const BB_BUBBLE_SPOOF_WEBGL As Integer = 10
    Public Const BB_BUBBLE_SPOOF_MATH As Integer = 11
    Public Const BB_BUBBLE_SPOOF_PERFTIMER As Integer = 12
    Public Const BB_BUBBLE_SPOOF_WEBRTC As Integer = 13
    ' RESERVED As Integer = 14
    Public Const BB_BUBBLE_SPOOF_MEDIA As Integer = 15
    Public Const BB_BUBBLE_SPOOF_SPEECH As Integer = 16
    Public Const BB_BUBBLE_SPOOF_BATTERY As Integer = 17
    Public Const BB_BUBBLE_SPOOF_NETWORK As Integer = 18
    Public Const BB_BUBBLE_SPOOF_CPU_ARCH As Integer = 19
    Public Const BB_BUBBLE_SPOOF_FIREFOX_VERSION As Integer = 20
    
    Public Const BB_NETWORK_FLAG_ETHERNET As Integer = 1
    Public Const BB_NETWORK_FLAG_WIFI As Integer = 2

    Public Const BB_BUBBLE_FLAG_ENCRYPT As Integer = 1
    Public Const BB_BUBBLE_FLAG_WIPE_ON_CLOSE As Integer = 2
    Public Const BB_BUBBLE_FLAG_CREATE_SHORTCUT As Integer = 4
    Public Const BB_BUBBLE_FLAG_BORDER_COLOR As Integer = 8
    Public Const BB_BUBBLE_FLAG_ANTI_EXPLOIT_READ As Integer = 16
    Public Const BB_BUBBLE_FLAG_ANTI_EXPLOIT_WRITE As Integer = 32
    Public Const BB_BUBBLE_FLAG_ANTI_EXPLOIT_EXECUTE As Integer = 64
    Public Const BB_BUBBLE_FLAG_DNS_BROWSER As Integer = 128
    Public Const BB_BUBBLE_FLAG_DNS_BB As Integer = 256
    Public Const BB_BUBBLE_FLAG_DNS_BLOCK As Integer = 512
    Public Const BB_BUBBLE_FLAG_PROXY_SET As Integer = 1024
    Public Const BB_BUBBLE_FLAG_VPN_SET As Integer = 2048
    Public Const BB_BUBBLE_FLAG_CLEAN_SLATE As Integer = 4096
    Public Const BB_BUBBLE_FLAG_DEBUG_PORT As Integer = 8192

    Public Const BB_ICON_DIRECTORY_NONE As Integer = 0
    Public Const BB_ICON_DIRECTORY_CURRENT_USER_DESKTOP As Integer = 1
    Public Const BB_ICON_DIRECTORY_ALL_USER_DESKTOP As Integer = 2
    Public Const BB_ICON_DIRECTORY_USER_DEFINED As Integer = 3
    
    Public Const BB_CPU_ARCH_NONE As Integer = 0
    Public Const BB_CPU_ARCH_ARM As Integer = 1
    Public Const BB_CPU_ARCH_I64 As Integer = 2
    Public Const BB_CPU_ARCH_X86 As Integer = 3
    Public Const BB_CPU_ARCH_ARM64 As Integer = 4
End Module
