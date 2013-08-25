package main

import (
  "fmt"
  "os"
  "io"
  "bufio"
)

const (
  FITS_PATH = "fits.fits"
  BYTES_PER_PIXEL = 2
  HEADER_LEN = 8000  // in bytes
)

func main() {
  fmt.Println("hello, world!")

  file, err := os.Open(FITS_PATH)
  if err != nil {
    fmt.Println(err)
    os.Exit(1)
  }
  defer file.Close()

  fmt.Printf("Read %s\n", file.Name())

  reader := bufio.NewReader(file)
  var (
    num_bytes = 0
    n int
    header [HEADER_LEN]byte
    bytes [BYTES_PER_PIXEL]byte
  )

  // Load header
  n, err = reader.Read(header[0:HEADER_LEN])
  if err != nil {
    fmt.Println(err)
    os.Exit(1)
  }
  if n < HEADER_LEN {
    fmt.Println("File too small to contain header")
    os.Exit(1)
  }

  // Load data
  for {
    n, err = reader.Read(bytes[0:BYTES_PER_PIXEL])
    if err == io.EOF || n == 0 {
      break
    } else if err != nil {
      fmt.Println(err)
      os.Exit(1)
    }
    num_bytes += n
  }

  fmt.Printf("# data bytes: %d\n", num_bytes)
}
