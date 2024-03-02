var baseWSUrl: string;

if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
  baseWSUrl = 'localhost:8000';
} else {
  baseWSUrl = window.location.host;
}

const capitalize = (string: string) => {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

export { capitalize, baseWSUrl }
