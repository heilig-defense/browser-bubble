<Serializable()>
Public Class BUBBLE_QUERY
    Public InstanceID As Long = 0
    Public Name As String = String.Empty
    Public BrowserID As Long = 0
    Public BrowserPID As Integer = 0
    Public DNSID As Long = 0
    Public ProxyList As New List(Of Long)
    Public VPNID As Long = 0
    Public ProfilePath As String = String.Empty
    Public PreLaunch As New LAUNCH_RESULT
    Public PostLaunch As New LAUNCH_RESULT
    Public Options As Integer = 0
    Public BorderColor As Integer = 0
    Public SpoofSettings As New Dictionary(Of Integer, String)
End Class
