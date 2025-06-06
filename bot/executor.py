import ctypes
import os
import ctypes.wintypes as wintypes
import platform



def run_stealth_command_linux(command: str) -> str:

    LIBC = ctypes.CDLL(None)
    EXECVE = LIBC.execve
    FORK = LIBC.fork
    WAITPID = LIBC.waitpid
    PIPE = LIBC.pipe
    DUP2 = LIBC.dup2
    READ = LIBC.read
    CLOSE = LIBC.close

    rpipe = ctypes.c_int()
    wpipe = ctypes.c_int()
    pipefd = (ctypes.c_int * 2)()
    if PIPE(pipefd) != 0:
        return "Pipe creation failed"

    rpipe, wpipe = pipefd[0], pipefd[1]

    pid = FORK()
    if pid == 0:
        # Child
        CLOSE(pipefd[0])
        DUP2(pipefd[1], 1)  # stdout
        DUP2(pipefd[1], 2)  # stderr
        CLOSE(pipefd[1])

        cmd = b"/bin/sh"
        args = (ctypes.c_char_p * 4)()
        args[0] = ctypes.c_char_p(cmd)
        args[1] = ctypes.c_char_p(b"-c")
        args[2] = ctypes.c_char_p(command.encode())
        args[3] = None

        env = (ctypes.c_char_p * 1)()
        env[0] = None

        EXECVE(ctypes.c_char_p(cmd), args, env)
        os._exit(1)
    else:
        CLOSE(pipefd[1])
        buffer = b""
        buf = ctypes.create_string_buffer(4096)
        while True:
            bytes_read = READ(pipefd[0], buf, 4096)
            if bytes_read <= 0:
                break
            buffer += buf.raw[:bytes_read]
        CLOSE(pipefd[0])
        WAITPID(pid, None, 0)
        return buffer.decode(errors="ignore")

    



def run_command_ctypes(command: str) -> str:


    CREATE_NO_WINDOW = 0x08000000
    STARTF_USESTDHANDLES = 0x00000100
    STARTF_USESHOWWINDOW = 0x00000001
    SW_HIDE = 0


    SECURITY_ATTRIBUTES = ctypes.Structure
    class SECURITY_ATTRIBUTES(ctypes.Structure):
        _fields_ = [
            ('nLength', wintypes.DWORD),
            ('lpSecurityDescriptor', wintypes.LPVOID),
            ('bInheritHandle', wintypes.BOOL)
        ]

    sa = SECURITY_ATTRIBUTES()
    sa.nLength = ctypes.sizeof(SECURITY_ATTRIBUTES)
    sa.lpSecurityDescriptor = None
    sa.bInheritHandle = True


    read_stdout = wintypes.HANDLE()
    write_stdout = wintypes.HANDLE()
    ctypes.windll.kernel32.CreatePipe(ctypes.byref(read_stdout), ctypes.byref(write_stdout), ctypes.byref(sa), 0)
    ctypes.windll.kernel32.SetHandleInformation(read_stdout, 1, 0)

    class STARTUPINFO(ctypes.Structure):
        _fields_ = [
            ('cb', wintypes.DWORD),
            ('lpReserved', wintypes.LPWSTR),
            ('lpDesktop', wintypes.LPWSTR),
            ('lpTitle', wintypes.LPWSTR),
            ('dwX', wintypes.DWORD),
            ('dwY', wintypes.DWORD),
            ('dwXSize', wintypes.DWORD),
            ('dwYSize', wintypes.DWORD),
            ('dwXCountChars', wintypes.DWORD),
            ('dwYCountChars', wintypes.DWORD),
            ('dwFillAttribute', wintypes.DWORD),
            ('dwFlags', wintypes.DWORD),
            ('wShowWindow', wintypes.WORD),
            ('cbReserved2', wintypes.WORD),
            ('lpReserved2', ctypes.POINTER(ctypes.c_byte)),
            ('hStdInput', wintypes.HANDLE),
            ('hStdOutput', wintypes.HANDLE),
            ('hStdError', wintypes.HANDLE),
        ]

    class PROCESS_INFORMATION(ctypes.Structure):
        _fields_ = [
            ('hProcess', wintypes.HANDLE),
            ('hThread', wintypes.HANDLE),
            ('dwProcessId', wintypes.DWORD),
            ('dwThreadId', wintypes.DWORD),
        ]

    si = STARTUPINFO()
    si.cb = ctypes.sizeof(si)
    si.dwFlags = STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW
    si.hStdOutput = write_stdout
    si.hStdError = write_stdout
    si.wShowWindow = SW_HIDE

    pi = PROCESS_INFORMATION()

    command_str = f'cmd.exe /c {command}'
    success = ctypes.windll.kernel32.CreateProcessW(
        None,
        ctypes.c_wchar_p(command_str),
        None,
        None,
        True,
        CREATE_NO_WINDOW,
        None,
        None,
        ctypes.byref(si),
        ctypes.byref(pi)
    )

    ctypes.windll.kernel32.CloseHandle(write_stdout)

    if not success:
        pass
        return "Failed to spawn process"


    output = b""
    buffer = ctypes.create_string_buffer(4096)
    bytes_read = wintypes.DWORD(0)

    while True:
        success = ctypes.windll.kernel32.ReadFile(read_stdout, buffer, 4096, ctypes.byref(bytes_read), None)
        if not success or bytes_read.value == 0:
            break
        output += buffer.raw[:bytes_read.value]


    ctypes.windll.kernel32.CloseHandle(read_stdout)
    ctypes.windll.kernel32.CloseHandle(pi.hProcess)
    ctypes.windll.kernel32.CloseHandle(pi.hThread)

    return output.decode("utf-8", errors="ignore")


def run_command_stealth(command:str):

    
    if platform.system() == "Windows":
        return run_command_ctypes(command)
    elif platform.system() == "Linux":
        return run_stealth_command_linux(command)


