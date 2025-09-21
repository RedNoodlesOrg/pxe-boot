using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

using pxe_boot_api_core.Data.Dto;
using pxe_boot_api_core.Data.Models;

namespace pxe_boot_api_core.Data.Repositories;

public class HostRepository(ApplicationDbContext context) : IRepositoryCrudBase<PxeHostDto>
{
    private readonly ApplicationDbContext _context = context;

    public async Task<ActionResult<PxeHostDto>> Create(PxeHostDto entity)
    {
        var host = new PxeHost()
        {
            Hostname = entity.Hostname,
            IPAddress = entity.IPAddress,
            Mac = entity.Mac
        };

        await _context.Hosts.AddAsync(host);
        await _context.SaveChangesAsync();

        return new PxeHostDto()
        {
            Id = host.Id,
            Hostname = host.Hostname,
            IPAddress = host.IPAddress,
            Mac = host.Mac
        };

    }

    public async Task<IActionResult> DeleteMany(long[] ids)
    {
        var entities = await _context.Hosts.AsNoTracking().Where(h => ids.Contains(h.Id)).ToListAsync();

        if (entities == null || entities.Count == 0)
        {
            return new StatusCodeResult(StatusCodes.Status404NotFound);
        }
        else if (entities.Count != ids.Length)
        {
            return new StatusCodeResult(StatusCodes.Status422UnprocessableEntity);
        }

        _context.Hosts.RemoveRange(entities);
        await _context.SaveChangesAsync();

        return new StatusCodeResult(StatusCodes.Status204NoContent);
    }
    public async Task<IActionResult> DeleteOne(long id)
    {
        var hostEntry = await _context.Hosts.FindAsync(id);
        if (hostEntry == null)
        {
            return new StatusCodeResult(StatusCodes.Status404NotFound);
        }

        _context.Hosts.Remove(hostEntry);
        await _context.SaveChangesAsync();

        return new StatusCodeResult(StatusCodes.Status204NoContent);
    }

    public async Task<ActionResult<IEnumerable<PxeHostDto>>> GetMany(long[] ids)
    {
        return await _context.Hosts.AsNoTracking().Where(h => ids.Contains(h.Id)).Select(h => new PxeHostDto()
        {
            Id = h.Id,
            IPAddress = h.IPAddress,
            Hostname = h.Hostname,
            Mac = h.Mac
        }).ToListAsync();
    }

    public async Task<ActionResult<PxeHostDto>> GetOne(long id)
    {
        var host = await _context.Hosts.FindAsync(id);

        if (host == null)
        {
            return new StatusCodeResult(StatusCodes.Status404NotFound);
        }

        return new PxeHostDto()
        {
            Id = host.Id,
            IPAddress = host.IPAddress,
            Hostname = host.Hostname,
            Mac = host.Mac
        };
    }

    public async Task<ActionResult<IEnumerable<PxeHostDto>>> List()
    {
        return await _context.Hosts.Select(h => new PxeHostDto()
        {
            Id = h.Id,
            IPAddress = h.IPAddress,
            Hostname = h.Hostname,
            Mac = h.Mac
        }).ToListAsync();
    }

    public async Task<IActionResult> UpdateMany(long[] ids, PxeHostDto entity)
    {
        foreach (long id in ids)
        {
            _context.Entry(new PxeHostDto()
            {
                Id = id,
                Hostname = entity.Hostname,
                IPAddress = entity.IPAddress,
                Mac = entity.Mac
            }).State = EntityState.Modified;
        }
        await _context.SaveChangesAsync();
        return new StatusCodeResult(StatusCodes.Status204NoContent);
    }

    public async Task<IActionResult> UpdateOne(long id, PxeHostDto entity)
    {
        if (id != entity.Id)
        {
            return new StatusCodeResult(StatusCodes.Status400BadRequest); ;
        }
        _context.Entry(entity).State = EntityState.Modified;
        await _context.SaveChangesAsync();
        return new StatusCodeResult(StatusCodes.Status204NoContent);
    }

}
