use eframe::egui;

fn main() -> Result<(), eframe::Error> {
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default().with_inner_size([1200.0, 800.0]),
        ..Default::default()
    };
    eframe::run_native(
        "HB Tools - PeopleTools IDE Clone",
        options,
        Box::new(|_cc| Box::new(HBIDE::default())),
    )
}

#[derive(Default)]
struct HBIDE {
    selected_tab: usize,
    code: String,
    project_files: Vec<String>,
}

impl eframe::App for HBIDE {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        egui::CentralPanel::default().show(ctx, |ui| {
            ui.heading("HB Tools - Integrated Development Environment");

            ui.horizontal(|ui| {
                ui.selectable_value(&mut self.selected_tab, 0, "Application Designer");
                ui.selectable_value(&mut self.selected_tab, 1, "PeopleCode Editor");
                ui.selectable_value(&mut self.selected_tab, 2, "Data Mover");
                ui.selectable_value(&mut self.selected_tab, 3, "Query Tool");
                ui.selectable_value(&mut self.selected_tab, 4, "Process Scheduler");
            });

            ui.separator();

            match self.selected_tab {
                0 => self.show_application_designer(ui),
                1 => self.show_peoplecode_editor(ui),
                2 => self.show_data_mover(ui),
                3 => self.show_query_tool(ui),
                4 => self.show_process_scheduler(ui),
                _ => {}
            }
        });
    }
}

impl HBIDE {
    fn show_application_designer(&mut self, ui: &mut egui::Ui) {
        ui.label("Application Designer - Visual design for pages, records, components");
        ui.label("Placeholder: Drag and drop components here");
        // TODO: Implement visual designer
    }

    fn show_peoplecode_editor(&mut self, ui: &mut egui::Ui) {
        ui.label("PeopleCode Editor");
        ui.add(egui::TextEdit::multiline(&mut self.code).hint_text("Write PeopleCode here..."));
    }

    fn show_data_mover(&mut self, ui: &mut egui::Ui) {
        ui.label("Data Mover - Import/Export data");
        ui.label("Placeholder: Select scripts and run");
        // TODO: Implement data mover interface
    }

    fn show_query_tool(&mut self, ui: &mut egui::Ui) {
        ui.label("Query Tool - Create and run queries");
        ui.label("Placeholder: Build queries here");
        // TODO: Implement query builder
    }

    fn show_process_scheduler(&mut self, ui: &mut egui::Ui) {
        ui.label("Process Scheduler - Schedule batch processes");
        ui.label("Placeholder: Manage scheduled processes");
        // TODO: Implement scheduler interface
    }
}
