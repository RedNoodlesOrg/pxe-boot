namespace pxe_boot_api_core;

public class HostEntry
{
    public long Id { get; set; }
    public string Hostname { get; set; }
    public string IPAddress { get; set; }
    public string Mac { get; set; }
}