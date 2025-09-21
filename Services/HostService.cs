using PXE_Boot_Api_Core.Data.Dto;
using PXE_Boot_Api_Core.Data.Repositories;
using PXE_Boot_Api_Core.Data.Results;

namespace PXE_Boot_Api_Core.Services;

public class HostService(IRepositoryCrudBase<PxeHostDto> repo) : IServicesCrudBase<PxeHostDto>
{
    private readonly IRepositoryCrudBase<PxeHostDto> _repo = repo;

    public async Task<Result<PxeHostDto>> Create(PxeHostDto entity)
    {
        if (string.IsNullOrEmpty(entity.Mac))
        {
            return Result<PxeHostDto>.FailureResult("Hostname cannot be empty.", ResultStatus.BadRequest);
        }
        else
        {
            return await _repo.Create(entity);
        }
    }

    public async Task<Result> DeleteOne(long id)
    {
        return await _repo.DeleteOne(id);
    }

    public async Task<Result> DeleteMany(long[] ids)
    {
        return await _repo.DeleteMany(ids);
    }

    public async Task<Result<PxeHostDto>> GetOne(long id)
    {
        return await _repo.GetOne(id);
    }

    public async Task<Result<IEnumerable<PxeHostDto>>> List()
    {
        return await _repo.List();
    }

    public async Task<Result> UpdateOne(long id, PxeHostDto entity)
    {
        return await _repo.UpdateOne(id, entity);
    }

    public async Task<Result> UpdateMany(long[] ids, PxeHostDto entity)
    {
        return await _repo.UpdateMany(ids, entity);
    }
}
