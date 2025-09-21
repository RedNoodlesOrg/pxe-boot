using PXE_Boot_Api_Core.Data.Results;

namespace PXE_Boot_Api_Core.Services;

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
