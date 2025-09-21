using pxe_boot_api_core.Data.Results;

public interface IResult
{
    ResultStatus Status { get; }
    string? Message { get; }
    object? Value { get; }
}
