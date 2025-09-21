using Microsoft.AspNetCore.Mvc;

using pxe_boot_api_core.Data.Dto;
using pxe_boot_api_core.Services;

namespace pxe_boot_api_core.Controllers;

[ApiController]
[Route("hosts")]
public class HostController(IServicesCrudBase<PxeHostDto> service) : CrudControllerBase<PxeHostDto>(service)
{
}
