using System;
using System.Collections.Generic;

[Serializable()]
public partial class BUBBLE_SAVED
{
    public long ID = 0L;
    public int IsInstance = 0;
    public string Name = string.Empty;
    public string ProfilePath = string.Empty;
    public long BrowserID = 0L;
    public long DNSID = 0L;
    public List<long> ProxyList = new List<long>();
    public long VPNID = 0L;
    public LAUNCH_ACTIONS Launch = new LAUNCH_ACTIONS();
    public int Options = 0;
    public int BorderColor = 0;
    public Dictionary<int, string> SpoofSettings = new Dictionary<int, string>();
}