#include <stdio.h>
#include <winsock2.h>
#include <ws2tcpip.h>

#pragma comment(lib, "ws2_32.lib")

// * Inisialisasi WinSock API untuk koneksi jaringan
int InitializeWinsock() {
    WSADATA wsaData;
    return WSAStartup(MAKEWORD(2, 2), &wsaData);
}

// * Tutup WinSock API setelah selesai digunakan
void CleanupWinsock() {
    WSACleanup();
}

// * Scan port tunggal pada target IP tertentu
int ScanPort(const char* targetIp, int port, int timeoutMs) {
    SOCKET sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock == INVALID_SOCKET) return -1;

    unsigned long mode = 1;
    ioctlsocket(sock, FIONBIO, &mode);

    struct sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(port);
    inet_pton(AF_INET, targetIp, &serverAddr.sin_addr);

    connect(sock, (struct sockaddr*)&serverAddr, sizeof(serverAddr));

    fd_set writeSet;
    FD_ZERO(&writeSet);
    FD_SET(sock, &writeSet);

    struct timeval timeout;
    timeout.tv_sec = timeoutMs / 1000;
    timeout.tv_usec = (timeoutMs % 1000) * 1000;

    int result = select(0, NULL, &writeSet, NULL, &timeout);
    closesocket(sock);

    return (result > 0) ? 1 : 0;
}
