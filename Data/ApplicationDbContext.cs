using Microsoft.EntityFrameworkCore;

using PXE_Boot_Api_Core.Data.Models;

namespace PXE_Boot_Api_Core.Data;

public class ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : DbContext(options)
{
    public DbSet<PxeHost> Hosts { get; set; } = default!;
    public DbSet<PxeProfile> Profiles { get; set; } = default!;
}
