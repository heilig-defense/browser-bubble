using System;

[Serializable()]
public partial class BROWSER_PROFILE
{
    public long ID = 0L;
    public string Name = string.Empty;
    public int BrowserType = 0;
    public string FilePath = string.Empty;
    public string ProfilePath = string.Empty;
    public int Enabled = 0;
}