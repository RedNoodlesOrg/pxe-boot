using PXE_Boot_Api_Core.Data.Results;

namespace PXE_Boot_Api_Core.Data.Repositories;

public interface IRepositoryCrudBase<T>
{
    Task<Result<IEnumerable<T>>> List();
    Task<Result<T>> GetOne(long id);
    Task<Result<IEnumerable<T>>> GetMany(long[] ids);
    Task<Result<T>> Create(T entity);
    Task<Result> UpdateOne(long id, T entity);
    Task<Result> DeleteOne(long id);
    Task<Result> UpdateMany(long[] ids, T entity);
    Task<Result> DeleteMany(long[] ids);
}
