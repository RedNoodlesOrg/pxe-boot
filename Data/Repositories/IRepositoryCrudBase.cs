using Microsoft.AspNetCore.Mvc;

namespace pxe_boot_api_core.Data.Repositories;

public interface IRepositoryCrudBase<T>
{
    Task<ActionResult<IEnumerable<T>>> List();
    Task<ActionResult<T>> GetOne(long id);
    Task<ActionResult<IEnumerable<T>>> GetMany(long[] ids);
    Task<ActionResult<T>> Create(T entity);
    Task<IActionResult> UpdateOne(long id, T entity);
    Task<IActionResult> DeleteOne(long id);
    Task<IActionResult> UpdateMany(long[] ids, T entity);
    Task<IActionResult> DeleteMany(long[] ids);
}
