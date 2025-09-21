using System.ComponentModel.DataAnnotations.Schema;

using Microsoft.EntityFrameworkCore;

namespace PXE_Boot_Api_Core.Data.Models;

[Table("hosts")]
[Index(nameof(Mac), IsUnique = true)]
public class PxeHost
{
    [Column("id")]
    public long Id { get; set; }
    [Column("hostname")]
    public string? Hostname { get; set; }
    [Column("ipaddress")]
    public string? IPAddress { get; set; }
    [Column("mac")]
    public string? Mac { get; set; }
}
