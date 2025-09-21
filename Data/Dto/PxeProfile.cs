namespace pxe_boot_api_core.Data.Dto;

public class PxeProfileDto
{
    public long? Id { get; set; }
    public string? Name { get; set; }
    public string? ButaneConfigPath { get; set; }
    public string? IgnitionConfigPath { get; set; }
}
