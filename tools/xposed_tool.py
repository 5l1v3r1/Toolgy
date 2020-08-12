# coding=utf-8

class XposedTool:
    def __init__(self):
        pass

    @staticmethod
    def generate_xposed_basic_code(xposed_panel):
        xposed_panel.textctrl_code.SetValue(
            '''public class Potat0Monitor implements IXposedHookLoadPackage {
    private static String TAG = "wnagzihxa1n";

    @Override
    public void handleLoadPackage(XC_LoadPackage.LoadPackageParam lpparam) throws Throwable {
        if ("".equals(lpparam.packageName)) {
            try {
                XposedHelpers.findAndHookMethod(className,
                        loadPackageParam.classLoader,
                        functionName, paramsType, new XC_MethodHook() {
                    @Override
                    protected void beforeHookedMethod(MethodHookParam param) throws Throwable {
                        super.beforeHookedMethod(param);
                    }

                    @Override
                    protected void afterHookedMethod(MethodHookParam param) throws Throwable {
                        super.afterHookedMethod(param);
                    }
                });
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}''')
