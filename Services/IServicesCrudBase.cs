using pxe_boot_api_core.Data.Results;

namespace pxe_boot_api_core.Services;

public interface IServicesCrudBase<T>
{
    Task<Result<IEnumerable<T>>> List();
    Task<Result<T>> GetOne(long id);
    Task<Result<T>> Create(T entity);
    Task<Result> UpdateOne(long id, T entity);
    Task<Result> UpdateMany(long[] ids, T entity);
    Task<Result> DeleteOne(long id);
    Task<Result> DeleteMany(long[] ids);
}
