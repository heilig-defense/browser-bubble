<Serializable()>
Public Class BUBBLE_UPDATE
    Public BubbleID As Long = 0
    Public Options As Integer = 0
    Public DNSID As Long = 0
    Public ProxyList As New List(Of Long)
    Public VPNID As Long = 0
    Public Launch As New LAUNCH_ACTIONS
    Public BorderColor As String = String.Empty
    Public SpoofSettings As New Dictionary(Of Integer, String)
End Class
