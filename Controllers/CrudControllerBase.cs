using Microsoft.AspNetCore.Mvc;

using PXE_Boot_Api_Core.Data.Results;
using PXE_Boot_Api_Core.Services;

using IResult = PXE_Boot_Api_Core.Data.Results.IResult;

namespace PXE_Boot_Api_Core.Controllers;

[ApiController]
public class CrudControllerBase<T>(IServicesCrudBase<T> service) : ControllerBase
{
    private readonly IServicesCrudBase<T> _service = service;

    [HttpGet]
    public async Task<ActionResult<IEnumerable<T>>> List() => HandleResult(await _service.List());
    [HttpGet("{id}")]
    public async Task<ActionResult<T>> GetOne(long id) => HandleResult(await _service.GetOne(id));

    [HttpPut("{id}")]
    public async Task<IActionResult> UpdateOne([FromQuery] long id, [FromBody] T entry) => HandleResult(await _service.UpdateOne(id, entry));

    [HttpPut]
    public async Task<IActionResult> UpdateMany([FromQuery] long[] ids, [FromBody] T entry) => HandleResult(await _service.UpdateMany(ids, entry));

    [HttpPost]
    public async Task<ActionResult<T>> Create([FromBody] T entry) => HandleResult(await _service.Create(entry));

    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteOne(long id) => HandleResult(await _service.DeleteOne(id));

    [HttpDelete]
    public async Task<IActionResult> DeleteMany([FromQuery] long[] ids) => HandleResult(await _service.DeleteMany(ids));

    private ActionResult HandleResult(IResult result)
    {
        if (result.Status == ResultStatus.Success && result.Value is not null)
        {
            return Ok(result.Value);
        }
        return result.Status switch
        {
            ResultStatus.Success => NoContent(),
            ResultStatus.NotFound => NotFound(result.Message),
            ResultStatus.BadRequest => BadRequest(result.Message),
            ResultStatus.Conflict => Conflict(result.Message),
            _ => StatusCode(500, "An unexpected error occurred.")
        };
    }

}
