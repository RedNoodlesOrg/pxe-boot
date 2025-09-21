namespace pxe_boot_api_core.Data.Dto;

public class PxeHostDto
{
    public long Id { get; set; }
    public string? Hostname { get; set; }
    public string? IPAddress { get; set; }
    public string? Mac { get; set; }
}
