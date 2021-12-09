<Serializable()>
Public Class BUBBLE_SAVED
    Public ID As Long = 0
    Public IsInstance As Integer = 0
    Public Name As String = String.Empty
    Public ProfilePath As String = String.Empty
    Public BrowserID As Long = 0
    Public DNSID As Long = 0
    Public ProxyList As New List(Of Long)
    Public VPNID As Long = 0
    Public Launch As New LAUNCH_ACTIONS
    Public Options As Integer = 0
    Public BorderColor As Integer = 0
    Public SpoofSettings As New Dictionary(Of Integer, String)
End Class
