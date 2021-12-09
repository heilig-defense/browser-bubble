using System;
using System.Collections.Generic;

[Serializable()]
public partial class BUBBLE_QUERY
{
    public long BrowserID = 0L;
    public int BrowserPID = 0;
    public long DNSID = 0L;
    public List<long> ProxyList = new List<long>();
    public long VPNID = 0L;
    public string ProfilePath = string.Empty;
    public LAUNCH_RESULT PreLaunch = new LAUNCH_RESULT();
    public LAUNCH_RESULT PostLaunch = new LAUNCH_RESULT();
    public int Options = 0;
    public int BorderColor = 0;
    public Dictionary<int, string> SpoofSettings = new Dictionary<int, string>();
}