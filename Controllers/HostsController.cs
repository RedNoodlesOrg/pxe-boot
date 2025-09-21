using Microsoft.AspNetCore.Mvc;

using PXE_Boot_Api_Core.Data.Dto;
using PXE_Boot_Api_Core.Services;

namespace PXE_Boot_Api_Core.Controllers;

[ApiController]
[Route("hosts")]
public class HostController(IServicesCrudBase<PxeHostDto> service) : CrudControllerBase<PxeHostDto>(service)
{
}
