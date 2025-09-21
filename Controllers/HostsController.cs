using Microsoft.AspNetCore.Mvc;

using pxe_boot_api_core.Data.Dto;
using pxe_boot_api_core.Data.Repositories;

namespace pxe_boot_api_core.Controllers
{
    [ApiController]
    [Route("hosts")]
    public class HostController(IRepositoryCrudBase<PxeHostDto> repo) : CrudControllerBase<PxeHostDto>(repo)
    {
    }
}
