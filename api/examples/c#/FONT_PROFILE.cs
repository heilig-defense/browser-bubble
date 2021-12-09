using System;
using System.Collections.Generic;

[Serializable()]
public partial class FONT_PROFILE
{
    public long FontID = 0L;
    public string Name = string.Empty;
    public List<FONT_ITEM> Fonts = new List<FONT_ITEM>();
}