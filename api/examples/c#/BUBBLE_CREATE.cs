using System;
using System.Collections.Generic;

[Serializable()]
public partial class BUBBLE_CREATE
{
    public string Name = string.Empty;
    public long BrowserID = 0L;
    public long DNSID = 0L;
    public List<long> ProxyList = new List<long>();
    public long VPNID = 0L;
    public LAUNCH_ACTIONS Launch = new LAUNCH_ACTIONS();
    public int Options = 0;
    public string BorderColor = string.Empty;
    public Dictionary<int, string> SpoofSettings = new Dictionary<int, string>();
}