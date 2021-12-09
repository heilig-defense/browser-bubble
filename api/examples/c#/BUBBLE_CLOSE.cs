using System;

[Serializable()]
public partial class BUBBLE_CLOSE
{
    public long InstanceID = 0L;
    public long BubbleID = 0L;
    public LAUNCH_RESULT ShutdownLaunch = new LAUNCH_RESULT();
}