public static partial class APIConsts
{
    public const int BB_SERVER_ACTION_STATUS = 0;
    public const int BB_SERVER_STATUS_SUB_ACTION_CURRENT = 1;
    public const int BB_SERVER_STATUS_SUB_ACTION_SHUTDOWN = 2;
    public const int BB_SERVER_STATUS_SUB_ACTION_LOG = 3;
    
    public const int BB_SERVER_ACTION_OPTIONS = 1;
    public const int BB_SERVER_OPTIONS_SUB_ACTION_SET_OP_VALUE = 1;
    public const int BB_SERVER_OPTIONS_SUB_ACTION_GET_OP_VALUE = 2;
    public const int BB_SERVER_OPTIONS_SUB_ACTION_REINIT = 3;
    
    public const int BB_SERVER_ACTION_BROWSER = 2;
    public const int BB_SERVER_BROWSER_SUB_ACTION_SYS_QUERY = 1;
    public const int BB_SERVER_BROWSER_SUB_ACTION_LIST = 2;
    public const int BB_SERVER_BROWSER_SUB_ACTION_ADD = 3;
    public const int BB_SERVER_BROWSER_SUB_ACTION_DELETE = 4;
    public const int BB_SERVER_BROWSER_SUB_ACTION_UPDATE = 5;
    
    public const int BB_SERVER_ACTION_SPEECH = 3;
    public const int BB_SERVER_SPEECH_SUB_ACTION_LIST = 1;
    public const int BB_SERVER_SPEECH_SUB_ACTION_CREATE = 2;
    public const int BB_SERVER_SPEECH_SUB_ACTION_DELETE = 3;
    public const int BB_SERVER_SPEECH_SUB_ACTION_UPDATE = 4;
    
    public const int BB_SERVER_ACTION_FONT = 4;
    public const int BB_SERVER_FONT_SUB_ACTION_LIST = 1;
    public const int BB_SERVER_FONT_SUB_ACTION_CREATE = 2;
    public const int BB_SERVER_FONT_SUB_ACTION_DELETE = 3;
    public const int BB_SERVER_FONT_SUB_ACTION_UPDATE = 4;
    public const int BB_SERVER_FONT_SUB_ACTION_INSTALL = 5;
    
    public const int BB_SERVER_ACTION_DNS = 5;
    public const int BB_SERVER_DNS_SUB_ACTION_SYNC = 1;
    public const int BB_SERVER_DNS_SUB_ACTION_LIST = 2;
    public const int BB_SERVER_DNS_SUB_ACTION_CREATE = 3;
    public const int BB_SERVER_DNS_SUB_ACTION_DELETE = 4;
    public const int BB_SERVER_DNS_SUB_ACTION_UPDATE = 5;
    public const int BB_SERVER_DNS_SUB_ACTION_SINKHOLE_SEARCH = 6;
    
    public const int BB_SERVER_ACTION_PROXY = 6;
    public const int BB_SERVER_PROXY_SUB_ACTION_LIST = 1;
    public const int BB_SERVER_PROXY_SUB_ACTION_CREATE = 2;
    public const int BB_SERVER_PROXY_SUB_ACTION_DELETE = 3;
    public const int BB_SERVER_PROXY_SUB_ACTION_UPDATE = 4;
    
    public const int BB_SERVER_ACTION_VPN = 7;
    public const int BB_SERVER_VPN_SUB_ACTION_LIST = 1;
    public const int BB_SERVER_VPN_SUB_ACTION_CREATE = 2;
    public const int BB_SERVER_VPN_SUB_ACTION_DELETE = 3;
    public const int BB_SERVER_VPN_SUB_ACTION_UPDATE = 4;
    
    public const int BB_SERVER_ACTION_BUBBLE = 8;
    public const int BB_SERVER_BUBBLE_SUB_ACTION_LIST_SAVED = 1;
    public const int BB_SERVER_BUBBLE_SUB_ACTION_LIST_RUNNING = 2;
    public const int BB_SERVER_BUBBLE_SUB_ACTION_CREATE = 3;
    public const int BB_SERVER_BUBBLE_SUB_ACTION_DELETE = 4;
    public const int BB_SERVER_BUBBLE_SUB_ACTION_UPDATE = 5;
    public const int BB_SERVER_BUBBLE_SUB_ACTION_DETAILS = 6;
    public const int BB_SERVER_BUBBLE_SUB_ACTION_GENERATE = 7;
    public const int BB_SERVER_BUBBLE_SUB_ACTION_SHORTCUT = 8;
    public const int BB_SERVER_BUBBLE_SUB_ACTION_LAUNCH = 9;
    public const int BB_SERVER_BUBBLE_SUB_ACTION_TERMINATE = 10;
    public const int BB_SERVER_BUBBLE_SUB_ACTION_NETWORK = 11;
    public const int BB_SERVER_BUBBLE_SUB_ACTION_READY = 12;
    public const int BB_SERVER_BUBBLE_SUB_ACTION_FAILED = 13;
    public const int BB_SERVER_BUBBLE_SUB_ACTION_SHUTDOWN = 14;
    public const int BB_SERVER_BUBBLE_SUB_ACTION_DEBUG_PORT = 15;
    
    public const int BB_SERVER_ACTION_LAUNCH = 9;
    public const int BB_SERVER_LAUNCH_SUB_ACTION_LIST = 1;
    public const int BB_SERVER_LAUNCH_SUB_ACTION_CREATE = 2;
    public const int BB_SERVER_LAUNCH_SUB_ACTION_DELETE = 3;
    public const int BB_SERVER_LAUNCH_SUB_ACTION_UPDATE = 4;
    
    public const int BB_OS_DISABLED = 0;
    public const int BB_OS_WIN7 = 1;
    public const int BB_OS_WIN8 = 2;
    public const int BB_OS_WIN81 = 4;
    public const int BB_OS_WIN10 = 8;
    public const int BB_OS_WIN11 = 16;
    public const int BB_OS_CUSTOM = 32;
    
    public const int BB_DATA_TYPE_STRING = 1;
    public const int BB_DATA_TYPE_INTEGER = 2;
    public const int BB_DATA_TYPE_JSON = 3;
    public const int BB_DATA_TYPE_BINARY = 4;
    public const int BB_DATA_TYPE_BASE64 = 5;
    
    public const int BB_ERROR_NO_ERROR = 0;
    public const int BB_ERROR_GENERIC_ERROR = -1;
    public const int BB_ERROR_INVALID_PARAMETER = -3;
    public const int BB_ERROR_INVALID_MODE = -26;
    public const int BB_ERROR_CREATING_PROCESS = -30;
    public const int BB_ERROR_NOT_READY = -34;
    public const int BB_ERROR_LICENSE_INVALID = -361;
    
    public const int BB_LOG_LEVEL_DEBUG = 1;
    public const int BB_LOG_LEVEL_ERROR = 2;
    public const int BB_LOG_LEVEL_INFO = 3;
    public const int BB_LOG_LEVEL_WARN = 4;
    public const int BB_LOG_LEVEL_PRIORITY = 5;
    
    public const int BB_OPTIONS_XET_FLAGS = 1;
    public const int BB_OPTIONS_XET_LICENSE = 2;
    public const int BB_OPTIONS_XET_ADAPTER = 3;
    public const int BB_OPTIONS_XET_ADAPTER_LIST = 4;
    public const int BB_OPTIONS_XET_GLOBAL_DNS = 5;
    public const int BB_OPTIONS_XET_GLOBAL_AEX = 6;
    
    public const int BB_OPTIONS_FLAG_AUTO_BUBBLE = 1;
    public const int BB_OPTIONS_FLAG_BLOCK_NET = 2;
    public const int BB_OPTIONS_FLAG_TERMINATE_ON_EXIT = 4;
    public const int BB_OPTIONS_FLAG_DELETE_PROFILE = 8;
    public const int BB_OPTIONS_FLAG_USE_VHD_SANDBOX = 16;
    public const int BB_OPTIONS_FLAG_VERBOSE_DNS_LOG = 32;
    
    public const int BB_LICENSE_STATUS_INVALID = 0;
    public const int BB_LICENSE_STATUS_VALID = 1;
    public const int BB_LICENSE_STATUS_TRIAL = 2;
    public const int BB_LICENSE_STATUS_EXPIRED = 3;
    public const int BB_LICENSE_STATUS_REVOKED = 4;
    
    public const int BB_LICENSE_ENTITLEMENT_SINGLE_SYSTEM = 1;
    public const int BB_LICENSE_ENTITLEMENT_MULTI_SYSTEM = 2;
    public const int BB_LICENSE_ENTITLEMENT_COUNT_LIMITED = 4;
    public const int BB_LICENSE_ENTITLEMENT_SERVER_ENABLED = 8;
    
    public const int BB_FONT_OP_PROFILE = 1;
    public const int BB_FONT_OP_FONT_ITEM = 2;

    public const int BB_GENERATE_COLOR_BORDER = 1;
    public const int BB_GENERATE_DEBUG_PORTS = 2;

    // Action is defined to run before the Bubble launches.
    public const int BB_LAUNCH_ACTION_OP_START_PRE = 1;
    // Action is defined to run right after the Bubble launches.
    public const int BB_LAUNCH_ACTION_OP_START_POST = 2;
    // Action is defined to run after the Bubble shuts down.
    public const int BB_LAUNCH_ACTION_OP_START_CLOSE = 4;
    // Browser Bubble will not wait for the process to finish.
    public const int BB_LAUNCH_ACTION_OP_WAIT_NONE = 8;
    // Browser Bubble will wait for the process to finish or until the 'Timeout' value is reached.
    public const int BB_LAUNCH_ACTION_OP_WAIT_COMPLETE = 16;
    // Browser Bubble will evaluate the output of the process in relation to the set 'EvalValue' field.
    public const int BB_LAUNCH_ACTION_OP_WAIT_EVAL = 32;
    // Output must match 'EvalValue' exactly.
    public const int BB_LAUNCH_ACTION_OP_EVAL_IS = 64;
    // Output must not match 'EvalValue' exactly.
    public const int BB_LAUNCH_ACTION_OP_EVAL_IS_NOT = 128;
    // Output must contain 'EvalValue'
    public const int BB_LAUNCH_ACTION_OP_EVAL_CONTAINS = 256;
    // Output must not contain 'EvalValue'
    public const int BB_LAUNCH_ACTION_OP_EVAL_CONTAINS_NOT = 512;
    // If the eval returns TRUE or the Timeout is reached then the Bubble will be cancelled.
    // If the eval returns FALSE then the Bubble will continue to launch.
    // This only applies for Pre actions.
    public const int BB_LAUNCH_ACTION_OP_ACTION_CANCEL = 1024;
    // If the eval returns FALSE or the Timeout is reached then the Bubble will continue to launch.
    // If the eval returns TRUE, then the Bubble will continue to launch.
    // This only applies for Pre actions.
    public const int BB_LAUNCH_ACTION_OP_ACTION_IGNORE = 2048;
    
    public const int BB_SPEECH_PROFILE = 1;
    public const int BB_SPEECH_VOICE = 2;
    public const int BB_SPEECH_PROFILE_VOICES = 3;
    public const int BB_SPEECH_AGE_ADULT = 1;
    public const int BB_SPEECH_AGE_CHILD = 2;
    public const int BB_SPEECH_SEX_FEMALE = 1;
    public const int BB_SPEECH_SEX_MALE = 2;
    public const int BB_BROWSER_FIREFOX = 1;
    public const int BB_BROWSER_EDGE = 2;
    public const int BB_BROWSER_CHROME = 4;
    public const int BB_BROWSER_BLISK = 8;
    public const int BB_BROWSER_BRAVE = 16;
    public const int BB_BROWSER_CANARY = 32;
    public const int BB_BROWSER_CHROMIUM = 64;
    public const int BB_BROWSER_IRIDIUM = 128;
    public const int BB_BROWSER_IRON = 256;
    public const int BB_BROWSER_OPERA = 512;
    public const int BB_BROWSER_VIVALDI = 1024;
    public const int BB_BROWSER_FIREFOX_NIGHTLY = 2048;
    public const int BB_BROWSER_EPIC = 4096;
    // User defined browsers.
    public const int BB_BROWSER_EXTRA_1 = 262144;
    public const int BB_BROWSER_EXTRA_2 = 524288;
    public const int BB_BROWSER_EXTRA_3 = 1048576;
    public const int BB_BROWSER_EXTRA_4 = 2097152;
    public const int BB_BROWSER_EXTRA_5 = 4194304;
    public const int BB_BROWSER_EXTRA_6 = 8388608;
    public const int BB_BROWSER_EXTRA_7 = 16777216;
    public const int BB_BROWSER_EXTRA_8 = 33554432;
    
    public const int BB_BROWSER_UPDATE_ENABLE = 1;
    public const int BB_BROWSER_UPDATE_PROFILE = 2;
    
    public const int BB_DNS_TYPE_DNS_OVER_TLS = 1;
    public const int BB_DNS_TYPE_DNS_OVER_HTTPS = 2;
    
    public const int BB_PROXY_TYPE_HTTPS = 1;
    public const int BB_PROXY_TYPE_SOCKS4 = 2;
    public const int BB_PROXY_TYPE_SOCKS5 = 3;
    
    public const int BB_BATTERY_FLAG_PLUGGED_IN = 1;
    public const int BB_BATTERY_FLAG_BATTERY_POWER = 2;
    public const int BB_BATTERY_FLAG_NO_BATTERY = 4;
    
    public const int BB_FONT_OPS_DISABLE = 1;
    public const int BB_FONT_OPS_REMOVE_ALL_BUT_1 = 2;
    public const int BB_FONT_OPS_REMOVE_ALL_BUT_DEFINED = 4;
    public const int BB_FONT_OPS_SET_OS = 8;
    public const int BB_FONT_OPS_SET_CUSTOM = 16;
    
    public const int BB_MATH_SPOOFING_OFF = 0;
    public const int BB_MATH_SPOOFING_RANDOM = 1;
    public const int BB_MATH_SPOOFING_SET = 2;
    
    public const int BB_MEDIA_DEVICE_SPOOF_OFF = 0;
    public const int BB_MEDIA_DEVICE_ENUM_RANDOM = 1;
    public const int BB_MEDIA_DEVICE_ENUM_BLOCK = 2;
    public const int BB_MEDIA_DEVICE_RENAME_NAMES = 4;
    public const int BB_MEDIA_DEVICE_SET_SAMPLE = 8;
    
    public const int BB_WEBGL_SPOOFING_OFF = 0;
    public const int BB_WEBGL_SET_FEATURE_LEVEL = 1;
    public const int BB_WEBGL_SET_IMAGE_RGB = 2;
    public const int BB_WEBGL_RANDOMIZE_IMAGE_RBG = 4;
    
    public const int BB_WEBGL_LEVEL_9_1 = 1;
    public const int BB_WEBGL_LEVEL_9_2 = 2;
    public const int BB_WEBGL_LEVEL_9_3 = 3;
    public const int BB_WEBGL_LEVEL_10_0 = 4;
    public const int BB_WEBGL_LEVEL_10_1 = 5;
    public const int BB_WEBGL_LEVEL_11_0 = 6;
    public const int BB_WEBGL_LEVEL_11_1 = 7;
    public const int BB_WEBGL_LEVEL_12_0 = 8;
    public const int BB_WEBGL_LEVEL_12_1 = 9;
    
    public const int BB_BUBBLE_SPOOF_TIMEZONE = 1;
    public const int BB_BUBBLE_SPOOF_SCREEN = 2;
    public const int BB_BUBBLE_SPOOF_CPU_COUNT = 3;
    public const int BB_BUBBLE_SPOOF_MEMORY = 4;
    public const int BB_BUBBLE_SPOOF_TOUCHPOINTS = 5;
    public const int BB_BUBBLE_SPOOF_FONTS = 6;
    public const int BB_BUBBLE_SPOOF_LANGUAGE = 7;
    public const int BB_BUBBLE_SPOOF_PLATFORM = 8;
    // RESERVED As Integer = 9
    public const int BB_BUBBLE_SPOOF_WEBGL = 10;
    public const int BB_BUBBLE_SPOOF_MATH = 11;
    public const int BB_BUBBLE_SPOOF_PERFTIMER = 12;
    public const int BB_BUBBLE_SPOOF_WEBRTC = 13;
    // RESERVED As Integer = 14
    public const int BB_BUBBLE_SPOOF_MEDIA = 15;
    public const int BB_BUBBLE_SPOOF_SPEECH = 16;
    public const int BB_BUBBLE_SPOOF_BATTERY = 17;
    public const int BB_BUBBLE_SPOOF_NETWORK = 18;
    public const int BB_BUBBLE_SPOOF_CPU_ARCH = 19;
    public const int BB_BUBBLE_SPOOF_FIREFOX_VERSION = 20;
    
    public const int BB_NETWORK_FLAG_ETHERNET = 1;
    public const int BB_NETWORK_FLAG_WIFI = 2;
    
    public const int BB_BUBBLE_FLAG_ENCRYPT = 1;
    public const int BB_BUBBLE_FLAG_WIPE_ON_CLOSE = 2;
    public const int BB_BUBBLE_FLAG_CREATE_SHORTCUT = 4;
    public const int BB_BUBBLE_FLAG_BORDER_COLOR = 8;
    public const int BB_BUBBLE_FLAG_ANTI_EXPLOIT_READ = 16;
    public const int BB_BUBBLE_FLAG_ANTI_EXPLOIT_WRITE = 32;
    public const int BB_BUBBLE_FLAG_ANTI_EXPLOIT_EXECUTE = 64;
    public const int BB_BUBBLE_FLAG_DNS_BROWSER = 128;
    public const int BB_BUBBLE_FLAG_DNS_BB = 256;
    public const int BB_BUBBLE_FLAG_DNS_BLOCK = 512;
    public const int BB_BUBBLE_FLAG_PROXY_SET = 1024;
    public const int BB_BUBBLE_FLAG_VPN_SET = 2048;
    public const int BB_BUBBLE_FLAG_CLEAN_SLATE = 4096;
    public const int BB_BUBBLE_FLAG_DEBUG_PORT = 8192;
    
    public const int BB_ICON_DIRECTORY_NONE = 0;
    public const int BB_ICON_DIRECTORY_CURRENT_USER_DESKTOP = 1;
    public const int BB_ICON_DIRECTORY_ALL_USER_DESKTOP = 2;
    public const int BB_ICON_DIRECTORY_USER_DEFINED = 3;
    
    public const int BB_CPU_ARCH_NONE = 0;
    public const int BB_CPU_ARCH_ARM = 1;
    public const int BB_CPU_ARCH_I64 = 2;
    public const int BB_CPU_ARCH_X86 = 3;
    public const int BB_CPU_ARCH_ARM64 = 4;
}
