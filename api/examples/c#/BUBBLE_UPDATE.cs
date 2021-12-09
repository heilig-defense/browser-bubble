using System;
using System.Collections.Generic;

[Serializable()]
public partial class BUBBLE_UPDATE
{
    public long BubbleID = 0L;
    public int Options = 0;
    public long DNSID = 0L;
    public List<long> ProxyList = new List<long>();
    public long VPNID = 0L;
    public LAUNCH_ACTIONS Launch = new LAUNCH_ACTIONS();
    public string BorderColor = string.Empty;
    public Dictionary<int, string> SpoofSettings = new Dictionary<int, string>();
}