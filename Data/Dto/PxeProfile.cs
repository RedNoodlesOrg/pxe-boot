namespace PXE_Boot_Api_Core.Data.Dto;

public class PxeProfileDto
{
    public long? Id { get; set; }
    public string? Name { get; set; }
    public string? ButaneConfigPath { get; set; }
    public string? IgnitionConfigPath { get; set; }
}
