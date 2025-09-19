using Microsoft.EntityFrameworkCore;
namespace pxe_boot_api_core;

public class HostsDbContext : DbContext
{
    public HostsDbContext(DbContextOptions<HostsDbContext> options)
        : base(options)
    {
    }
}