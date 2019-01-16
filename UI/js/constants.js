export const ireporterSettings = {
  base_url: 'https://ireporter-ao.herokuapp.com/api/v2',
};

// export ireporterSettings;

export const defaultHeaders = new Headers({
  'Content-Type': 'application/json',
});

const constants = {
  ireporterSettings,
  defaultHeaders,
};

export default constants;
