using Microsoft.AspNetCore.Mvc;

using pxe_boot_api_core.Data.Repositories;

namespace pxe_boot_api_core.Controllers
{
    [ApiController]
    public class CrudControllerBase<T>(IRepositoryCrudBase<T> repo) : ControllerBase
    {
        private readonly IRepositoryCrudBase<T> _repo = repo;

        [HttpGet]
        public async Task<ActionResult<IEnumerable<T>>> List() => await _repo.List();
        [HttpGet("{id}")]
        public async Task<ActionResult<T>> GetOne(long id) => await _repo.GetOne(id);

        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateOne(long id, T entry) => await _repo.UpdateOne(id, entry);

        [HttpPost]
        public async Task<ActionResult<T>> Create(T entry) => await _repo.Create(entry);

        [HttpDelete("{id}")]
        public async Task<IActionResult> Delete(long id) => await _repo.DeleteOne(id);

    }
}
