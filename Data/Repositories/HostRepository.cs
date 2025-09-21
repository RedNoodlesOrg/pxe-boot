using Microsoft.EntityFrameworkCore;

using PXE_Boot_Api_Core.Data.Dto;
using PXE_Boot_Api_Core.Data.Models;
using PXE_Boot_Api_Core.Data.Results;

namespace PXE_Boot_Api_Core.Data.Repositories;

public class HostRepository(ApplicationDbContext context) : IRepositoryCrudBase<PxeHostDto>
{
    private readonly ApplicationDbContext _context = context;

    public async Task<Result<PxeHostDto>> Create(PxeHostDto entity)
    {
        var host = new PxeHost()
        {
            Hostname = entity.Hostname,
            IPAddress = entity.IPAddress,
            Mac = entity.Mac
        };

        await _context.Hosts.AddAsync(host);
        await _context.SaveChangesAsync();

        return Result<PxeHostDto>.SuccessResult(new PxeHostDto()
        {
            Id = host.Id,
            IPAddress = host.IPAddress,
            Hostname = host.Hostname,
            Mac = host.Mac
        });

    }

    public async Task<Result> DeleteMany(long[] ids)
    {
        var entities = await _context.Hosts.AsNoTracking().Where(h => ids.Contains(h.Id)).ToListAsync();

        if (entities == null || entities.Count == 0)
        {
            return Result.NotFound();
        }
        else if (entities.Count != ids.Length)
        {
            return Result.FailureResult("Amount of found entities does not match the number of given id's.");
        }

        _context.Hosts.RemoveRange(entities);
        await _context.SaveChangesAsync();

        return Result.SuccessResult();
    }
    public async Task<Result> DeleteOne(long id)
    {
        var hostEntry = await _context.Hosts.FindAsync(id);
        if (hostEntry == null)
        {
            return Result.NotFound();
        }

        _context.Hosts.Remove(hostEntry);
        await _context.SaveChangesAsync();

        return Result.SuccessResult();
    }

    public async Task<Result<IEnumerable<PxeHostDto>>> GetMany(long[] ids)
    {
        var hosts = await _context.Hosts.AsNoTracking().Where(h => ids.Contains(h.Id)).Select(h => new PxeHostDto()
        {
            Id = h.Id,
            IPAddress = h.IPAddress,
            Hostname = h.Hostname,
            Mac = h.Mac
        }).ToListAsync();
        return Result<IEnumerable<PxeHostDto>>.With(hosts != null && hosts.Count > 0, hosts, "No host found", ResultStatus.NotFound);
    }

    public async Task<Result<PxeHostDto>> GetOne(long id)
    {
        var host = await _context.Hosts.FindAsync(id);

        if (host == null)
        {
            return Result<PxeHostDto>.FailureResult("HostId not found");
        }

        return Result<PxeHostDto>.SuccessResult(new PxeHostDto()
        {
            Id = host.Id,
            IPAddress = host.IPAddress,
            Hostname = host.Hostname,
            Mac = host.Mac
        });
    }

    public async Task<Result<IEnumerable<PxeHostDto>>> List()
    {
        var hosts = await _context.Hosts.AsNoTracking().Select(h => new PxeHostDto()
        {
            Id = h.Id,
            IPAddress = h.IPAddress,
            Hostname = h.Hostname,
            Mac = h.Mac
        }).ToListAsync();
        return Result<IEnumerable<PxeHostDto>>.With(hosts != null, hosts, "Query failed");
    }

    // This method makes no sense, every host is unique.
    public async Task<Result> UpdateMany(long[] ids, PxeHostDto entity)
    {
        var hosts = await _context.Hosts.AsNoTracking().Where(h => ids.Contains(h.Id)).ToListAsync();
        foreach (var host in hosts)
        {
            if (entity.Hostname is not null) host.Hostname = entity.Hostname;
            if (entity.IPAddress is not null) host.IPAddress = entity.Hostname;
            _context.Entry(host).State = EntityState.Modified;
        }
        await _context.SaveChangesAsync();
        return Result.SuccessResult();
    }

    public async Task<Result> UpdateOne(long id, PxeHostDto entity)
    {
        if (id != entity.Id)
        {
            return Result.FailureResult("Id in query does not match Id in body", ResultStatus.BadRequest);
        }
        _context.Entry(entity).State = EntityState.Modified;
        await _context.SaveChangesAsync();
        return Result.SuccessResult();
    }

}
