namespace PXE_Boot_Api_Core.Data.Results;
public interface IResult
{
    ResultStatus Status { get; }
    string? Message { get; }
    object? Value { get; }
}
