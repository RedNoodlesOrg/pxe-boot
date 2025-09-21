namespace PXE_Boot_Api_Core.Data.Dto;

public class PxeHostDto
{
    public long Id { get; set; }
    public string? Hostname { get; set; }
    public string? IPAddress { get; set; }
    public string? Mac { get; set; }
}
