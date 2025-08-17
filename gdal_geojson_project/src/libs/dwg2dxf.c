#include <stdio.h>
#include <stdlib.h>
#include <libredwg.h>

int main(int argc, char *argv[]) {
    if (argc != 3) {
        printf("Usage: %s input.dwg output.dxf\n", argv[0]);
        return 1;
    }

    const char *input_path = argv[1];
    const char *output_path = argv[2];

    Dwg_Data dwg;
    int ret = dwg_read_file(input_path, &dwg);
    if (ret != 0) {
        fprintf(stderr, "Failed to read DWG file: %s\n", input_path);
        return 2;
    }

    ret = dwg_write_dxf(output_path, &dwg, 2013, 0);  // 2013 = AC1027
    if (ret != 0) {
        fprintf(stderr, "Failed to write DXF file: %s\n", output_path);
        dwg_free(&dwg);
        return 3;
    }

    printf("Successfully converted to DXF: %s\n", output_path);
    dwg_free(&dwg);
    return 0;
}
