using Microsoft.EntityFrameworkCore;

using pxe_boot_api_core.Data;
using pxe_boot_api_core.Data.Dto;
using pxe_boot_api_core.Data.Repositories;
using pxe_boot_api_core.Services;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDbContext<ApplicationDbContext>(opt => opt.UseInMemoryDatabase("HostsContext"));
builder.Services.AddScoped<IRepositoryCrudBase<PxeHostDto>, HostRepository>();
builder.Services.AddScoped<IServicesCrudBase<PxeHostDto>, HostService>();
builder.Services.AddControllers();
builder.Services.AddOpenApi();
var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
    app.UseSwaggerUi(options =>
    {
        options.DocumentPath = "/openapi/v1.json";
    });

}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();
