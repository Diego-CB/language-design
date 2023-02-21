def toFileName(filename:str) -> str:
  filename = filename.replace('*', '_kleen_')
  filename = filename.replace('+', '_kleen_')
  filename = filename.replace('?', '_kleen_')
  filename = filename.replace('|', '_or_')

  return filename