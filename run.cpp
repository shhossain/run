#include <iostream>
using namespace std;

// pass all terminal argiments to python script
int main(int argc, char *argv[])
{
    // get current file path
    string file_path = argv[0];
    string file_dir = file_path.substr(0, file_path.find_last_of("\\/"));
    string py_file_path = file_dir + "\\main.py";

    cout << "Je";

    string cmd = "py " + py_file_path;
    for (int i = 1; i < argc; i++)
    {
        cmd += " ";
        cmd += argv[i];
    }
    system(cmd.c_str());
    return 0;
}