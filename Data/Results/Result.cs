namespace pxe_boot_api_core.Data.Results;

public class Result<T> : IResult
{
    public ResultStatus Status { get; private set; }
    public T? Value { get; private set; }
    public string? Message { get; private set; }
    object? IResult.Value => Value;

    // Private constructor to force use of factory methods
    private Result(ResultStatus status, T? value, string? message)
    {
        Status = status;
        Value = value;
        Message = message;
    }

    // Factory method for a successful result
    public static Result<T> SuccessResult(T value) => new(ResultStatus.Success, value, null);

    // Factory method for a failed result
    public static Result<T> FailureResult(string message, ResultStatus status = ResultStatus.Failure) => new(status, default, message);
    
    // New With method
    public static Result<T> With(bool condition, T? value, string failureMessage, ResultStatus status = ResultStatus.Failure) =>
        condition && value is not null ? SuccessResult(value) : FailureResult(failureMessage, status);
}

public class Result : IResult
{
    public ResultStatus Status { get; private set; }
    public string? Message { get; private set; }

    public object? Value => null;

    private Result(ResultStatus status, string? message, object? value = null)
    {
        Status = status;
        Message = message;
    }

    public static Result SuccessResult() => new(ResultStatus.Success, null);

    public static Result FailureResult(string message, ResultStatus status = ResultStatus.Failure) => new(status, message);

    // New With method
    public static Result With(bool condition, string failureMessage, ResultStatus status = ResultStatus.Failure) =>
        condition ? SuccessResult() : FailureResult(failureMessage, status);

    public static Result NotFound() => new(ResultStatus.NotFound, null);
}