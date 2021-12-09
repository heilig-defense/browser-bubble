using System;

[Serializable()]
public partial class BUBBLE_READY
{
    public long InstanceID = 0L;
    public long BubbleID = 0L;
    public string MountPoint = string.Empty;
    public LAUNCH_RESULT PreLaunch = new LAUNCH_RESULT();
    public LAUNCH_RESULT PostLaunch = new LAUNCH_RESULT();
}