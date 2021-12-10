package main

type SERVER_RESPONSE struct {
	ErrorCode   int
	DataType    int
	Version     int
	MessageId   int64
	ReturnValue string
}

type SERVER_REQUEST struct {
	Version      int
	MessageId    int64
	DataType     int
	RequestValue string
}

type ACTION struct {
	Action      int
	SubAction   int
	ValueString string
}

type PROFILE_LAUNCH struct {
	Pre      string
	Post     string
	Shutdown string
}

type LAUNCH_RESULT struct {
	ErrorCode int
	Output    string
	Eval      int
}

type BROWSER struct {
	ID          int64
	Name        string
	Enabled     int
	BrowserType int
	FilePath    string
	ProfilePath string
}

type BUBBLE_CLOSE struct {
	InstanceID     int64
	BubbleID       int64
	ShutdownLaunch LAUNCH_RESULT
}

type BUBBLE_CREATE struct {
	Name          string
	BrowserID     int64
	DNSID         int64
	ProxyList     []int64
	VPNID         int64
	Launch        PROFILE_LAUNCH
	Options       int
	BorderColor   string
	SpoofSettings map[int]string
}

type BUBBLE_DELETE struct {
	ID         int64
	IsInstance int
	Wipe       int
}

type BUBBLE_FAIL struct {
	ProcessId   int
	BrowserPath string
	ErrorCode   int
	Log         string
}

type BUBBLE_GENERATE struct {
	BrowserID    int64
	Count        int
	IconLocation int
	IconPath     string
}

type BUBBLE_LAUNCH struct {
	ID         int64
	IsInstance int
	Flags      int
	Password   string
	DNSID      int64
	ProxyList  []int64
	VPNID      int64
}

type BUBBLE_QUERY struct {
	InstanceID    int64
	Name          string
	BrowserID     int64
	BrowserPID    int
	DNSID         int64
	ProxyList     []int64
	VPNID         int64
	ProfilePath   string
	PreLaunch     LAUNCH_RESULT
	PostLaunch    LAUNCH_RESULT
	Options       int
	BorderColor   int
	SpoofSettings map[int]string
}

type BUBBLE_READY struct {
	InstanceID int64
	BubbleID   int64
	MountPoint string
	PreLaunch  LAUNCH_RESULT
	PostLaunch LAUNCH_RESULT
}

type BUBBLE_RUNNING struct {
	InstanceID int64
	BubbleID   int64
	DTG        int64
}

type BUBBLE_SAVED struct {
	ID            int64
	IsInstance    int
	Name          string
	ProfilePath   string
	BrowserID     int64
	DNSID         int64
	ProxyList     []int64
	VPNID         int64
	Launch        PROFILE_LAUNCH
	Options       int
	BorderColor   int
	SpoofSettings map[int]string
}

type BUBBLE_SHORTCUT struct {
	ID           int64
	Name         string
	IsInstance   int
	IconLocation int
	IconPath     string
}

type BUBBLE_SHUTDOWN struct {
	InstanceID     int64
	BubbleID       int64
	ShutdownLaunch LAUNCH_RESULT
}

type BUBBLE_TERMINATE struct {
	InstanceID int64
	Wipe       int
}

type BUBBLE_UPDATE struct {
	BubbleID      int64
	Options       int
	DNSID         int64
	ProxyList     []int64
	VPNID         int64
	Launch        PROFILE_LAUNCH
	BorderColor   string
	SpoofSettings map[int]string
}

type DNS_SERVER struct {
	ProviderID int64
	Provider   string
	ServerID   int64
	Country    string
	DNSType    int
	Address    string
	Port       int
}

type DNS_OP struct {
	DNS  int
	ID   int64
	Data string
}

type FONT_INSTALL struct {
	OS       int
	FontPath string
}

type FONT_RESPONSE struct {
	Op   int
	Data string
}

type FONT_ITEM struct {
	FontFileID int64
	FontName   string
	FontPath   string
}

type FONT_PROFILE struct {
	FontID int64
	Name   string
	Fonts  []FONT_ITEM
}

type LICENSE struct {
	LicenseKey    string
	Status        int
	Expires       string
	Entitlements  int64
	EndpointCount int64
}

type LOG_MESSAGE struct {
	ErrorCode int
	Level     int
	Location  string
	Message   string
}

type BROWSER_OPS struct {
	Op   int
	Id   int64
	Data string
}

type BROWSER_INSTALL struct {
	BrowserType int
	BrowserName string
	FilePath    string
	ProfilePath string
	ProfileName string
}

type SPEECH_OPS struct {
	Op   int
	Id   int64
	Data string
}

type COUNTRY_ITEM struct {
	Code string
	Name string
}

type VPN struct {
	ID       int
	Provider string
	Country  COUNTRY_ITEM
	Address  string
	Adapter  string
}

type OPS_SET struct {
	Op    int
	SubOp int
	Data  string
}

type SPOOF_BATTERY struct {
	Flags   int
	Values1 int
	Values2 int
	Values3 int
}

type SPOOF_FONT struct {
	Flags int
	Extra int64
}

type SPOOF_MATH struct {
	Flag   int
	Offset int
}

type SPOOF_MEDIA struct {
	Flags  int
	SetVal int
}

type SPOOF_OS struct {
	Windows int
	Build   int
}

type SPOOF_WGL struct {
	Offset int
	Level  int
	Spoof  int
}
