using Microsoft.EntityFrameworkCore;

using pxe_boot_api_core.Data.Models;

namespace pxe_boot_api_core.Data;

public class ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : DbContext(options)
{
    public DbSet<PxeHost> Hosts { get; set; } = default!;
    public DbSet<PxeProfile> Profiles { get; set; } = default!;
}
