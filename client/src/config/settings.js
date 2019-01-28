const settings = {
  IS_PROD: process.env.NODE_ENV === 'production',
  API_ROOT: process.env.API_ROOT,
  gaTrackingID: 'UA-119141143-4',
};

export default settings;
