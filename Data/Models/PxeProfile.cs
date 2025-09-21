using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace PXE_Boot_Api_Core.Data.Models;

[Table("profiles")]
public class PxeProfile
{
    [Column("id")]
    public long Id { get; set; }
    [Column("name")]
    [MaxLength(255)]
    public required string Name { get; set; }
    [Column("butane_config_path")]
    [MaxLength(500)]
    public string? ButaneConfigPath { get; set; }
    [Column("butane_last_edited")]
    public DateTime? ButaneLastEdited { get; set; }
    [Column("ignition_config_path")]
    [MaxLength(500)]
    public string? IgnitionConfigPath { get; set; }
    [Column("ignition_last_edited")]
    public DateTime? IgnitionLastEdited { get; set; }
}
