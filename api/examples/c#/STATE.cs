using System;
using System.Collections.Generic;

[Serializable()]
public partial class STATE
{
    public int License = 0;
    public int Drivers = 0;
    public int Browsers = 0;
    public int Options = 0;
    public Dictionary<int, string> InitErrors = new Dictionary<int, string>();
    public int Update = 0;
    public string UpdateVersion = string.Empty;
    public string UpdateMessage = string.Empty;
    public int SavedBubbles = 0;
    public int RunningBubbles = 0;
}